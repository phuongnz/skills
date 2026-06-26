/* ===========================================================================
   md.js — tiny self-contained Markdown renderer for teach-me-now
   ---------------------------------------------------------------------------
   Why home-grown instead of marked.js? So the workspace has ZERO network
   dependency and works when opened directly via file://. It covers the subset
   of Markdown the foundation docs use: headings, bold/italic, inline code,
   links, ordered/unordered lists, blockquotes, fenced code, hr, tables.

   Usage (see templates/doc.html):
       <script id="md" type="text/markdown"> ...markdown... </script>
       <div id="out"></div>
       <script>TMN.render('md', 'out');</script>
   =========================================================================== */
(function (global) {
  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // Inline: code spans first (protected behind an @@CODEn@@ sentinel so they
  // survive escaping and the bold/italic passes), then links, bold, italic.
  // The sentinel has no &<>*_ and is not digit-only, so no pass touches it and
  // it won't collide with ordinary numbers in the prose.
  function inline(s) {
    var codes = [];
    s = s.replace(/`([^`]+)`/g, function (_, c) {
      codes.push('<code>' + esc(c) + '</code>');
      return '@@CODE' + (codes.length - 1) + '@@';
    });
    s = esc(s);
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener">$1</a>');
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/(^|[^*])\*([^*]+)\*/g, '$1<em>$2</em>');
    s = s.replace(/(^|[^_])_([^_]+)_/g, '$1<em>$2</em>');
    s = s.replace(/@@CODE(\d+)@@/g, function (_, i) { return codes[+i]; });
    return s;
  }

  function parse(src) {
    // Normalise & strip a common leading indent (markdown is embedded indented in HTML).
    var lines = src.replace(/\r\n?/g, '\n').replace(/\t/g, '    ').split('\n');
    while (lines.length && !lines[0].trim()) lines.shift();
    while (lines.length && !lines[lines.length - 1].trim()) lines.pop();
    var indent = Infinity;
    lines.forEach(function (l) {
      if (l.trim()) indent = Math.min(indent, l.match(/^ */)[0].length);
    });
    if (indent === Infinity) indent = 0;
    lines = lines.map(function (l) { return l.slice(indent); });

    var html = [], i = 0;
    function flushTable(rows) {
      var out = '<table>';
      rows.forEach(function (r, ri) {
        if (ri === 1 && /^[\s|:-]+$/.test(r)) return; // separator row
        var cells = r.replace(/^\||\|$/g, '').split('|');
        var tag = ri === 0 ? 'th' : 'td';
        out += '<tr>' + cells.map(function (c) {
          return '<' + tag + '>' + inline(c.trim()) + '</' + tag + '>';
        }).join('') + '</tr>';
      });
      return out + '</table>';
    }

    while (i < lines.length) {
      var line = lines[i];

      if (!line.trim()) { i++; continue; }

      // Fenced code
      if (/^```/.test(line)) {
        var buf = []; i++;
        while (i < lines.length && !/^```/.test(lines[i])) buf.push(lines[i++]);
        i++;
        html.push('<pre><code>' + esc(buf.join('\n')) + '</code></pre>');
        continue;
      }
      // Heading
      var h = line.match(/^(#{1,4})\s+(.*)$/);
      if (h) { var n = h[1].length; html.push('<h' + n + '>' + inline(h[2]) + '</h' + n + '>'); i++; continue; }
      // HR
      if (/^(\*{3,}|-{3,}|_{3,})\s*$/.test(line)) { html.push('<hr>'); i++; continue; }
      // Blockquote
      if (/^>\s?/.test(line)) {
        var q = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) q.push(lines[i++].replace(/^>\s?/, ''));
        html.push('<blockquote>' + parse(q.join('\n')) + '</blockquote>');
        continue;
      }
      // Table (a row with | and a separator on the next line)
      if (/\|/.test(line) && i + 1 < lines.length && /^[\s|:-]+$/.test(lines[i + 1]) && /\|/.test(lines[i + 1])) {
        var trows = [];
        while (i < lines.length && /\|/.test(lines[i])) trows.push(lines[i++]);
        html.push(flushTable(trows));
        continue;
      }
      // Lists
      var ul = line.match(/^[-*]\s+(.*)$/);
      var ol = line.match(/^\d+\.\s+(.*)$/);
      if (ul || ol) {
        var tag = ul ? 'ul' : 'ol', items = [];
        var re = ul ? /^[-*]\s+(.*)$/ : /^\d+\.\s+(.*)$/;
        while (i < lines.length) {
          var m = lines[i].match(re);
          if (m) { items.push(m[1]); i++; }
          else if (/^\s+\S/.test(lines[i]) && items.length) { // wrapped continuation line
            items[items.length - 1] += '\n' + lines[i].replace(/^\s+/, ' '); i++;
          } else break;
        }
        html.push('<' + tag + '>' + items.map(function (it) {
          return '<li>' + inline(it) + '</li>';
        }).join('') + '</' + tag + '>');
        continue;
      }
      // Paragraph
      var p = [];
      while (i < lines.length && lines[i].trim() &&
             !/^(#{1,4}\s|>|```|[-*]\s|\d+\.\s)/.test(lines[i]) &&
             !/^(\*{3,}|-{3,}|_{3,})\s*$/.test(lines[i])) {
        p.push(lines[i++]);
      }
      html.push('<p>' + inline(p.join(' ')) + '</p>');
    }
    return html.join('\n');
  }

  function render(srcId, outId) {
    var src = document.getElementById(srcId);
    var out = document.getElementById(outId || 'out');
    if (!src || !out) return;
    out.innerHTML = parse(src.textContent);
    var first = out.querySelector('h1');
    if (first && !document.title.trim()) document.title = first.textContent;
  }

  global.TMN = { parse: parse, render: render };
})(window);
