/* submit.js — hands what the learner answered on this page to the tutor.
   Included by lesson and assessment pages; reads the .quiz blocks (and a lesson's
   .challenge) as they are, so pages need no extra markup. Served, a "Send to tutor"
   button appears after the last block; opened off disk there is no server, so
   nothing shows and the learner reports by hand as before.

   Sending does two things: bin/study-server.py writes the answers to
   submissions/<date>-<kind>.md, then the console types a one-line note into the
   tutor's drawer, which points at that file. If the drawer cannot take it, the
   note here tells the learner to mention the file instead. */
(function () {
  if (location.protocol !== "http:" && location.protocol !== "https:") return;

  var text = function (el) { return el ? el.textContent.replace(/\s+/g, " ").trim() : ""; };
  var kind = document.body.dataset.kind ||
    location.pathname.split("/").pop().replace(/\.html$/, "") || "page";

  /* One record per block. A quiz is "choice" (buttons) or "short" (textarea + model
     answer); a lesson's challenge is the learner's own summary against a model. */
  function collect() {
    var items = [];
    document.querySelectorAll(".quiz").forEach(function (q, i) {
      var item = { n: i + 1, topic: q.dataset.topic || "", question: text(q.querySelector("p")) };
      var ta = q.querySelector("textarea");
      if (ta) {
        item.type = "short";
        item.answer = ta.value.trim();
        item.model = text(q.querySelector(".model p"));
        item.outcome = q.dataset.outcome || (item.answer ? "unmarked" : "open");
      } else {
        item.type = "choice";
        item.correct = text(q.querySelector("button[data-right]"));
        var wrong = Array.prototype.map.call(q.querySelectorAll("button.wrong"), text);
        var gotRight = !!q.querySelector("button[data-right].right");
        item.picked = wrong.concat(gotRight ? [item.correct] : []);
        item.outcome = q.dataset.outcome ||
          (!item.picked.length ? "open" : gotRight && !wrong.length ? "right" :
            gotRight ? "right after " + wrong.length + " wrong" : "missed");
      }
      items.push(item);
    });
    var ch = document.querySelector(".challenge");
    if (ch) {
      var v = ch.querySelector("textarea");
      items.push({ n: items.length + 1, topic: "", type: "challenge",
        question: text(ch.querySelector("p")), answer: v ? v.value.trim() : "",
        model: text(ch.querySelector(".model p")),
        outcome: v && v.value.trim() ? "unmarked" : "open" });
    }
    return items;
  }
  function answered(items) {
    return items.filter(function (it) { return it.outcome !== "open"; }).length;
  }

  /* The button sits after the result block, the challenge, or the last quiz. */
  var anchor = document.querySelector(".result") || document.querySelector(".challenge") ||
    Array.prototype.slice.call(document.querySelectorAll(".quiz")).pop();
  if (!anchor) return;
  var box = document.createElement("div");
  box.className = "submit";
  box.innerHTML = '<button type="button" id="submit-btn" disabled>Send to tutor</button>' +
    '<span class="submit-note" id="submit-note"></span>';
  anchor.insertAdjacentElement("afterend", box);
  var btn = document.getElementById("submit-btn"), note = document.getElementById("submit-note");

  function refresh() {
    var items = collect(), n = answered(items);
    btn.disabled = !n;
    note.textContent = n ? n + " of " + items.length + " answered — sends your answers to the drawer."
      : "Answer something first.";
  }
  document.addEventListener("click", function () { setTimeout(refresh, 0); });
  document.addEventListener("input", refresh);
  refresh();

  btn.addEventListener("click", function () {
    btn.disabled = true;
    note.textContent = "Sending…";
    var payload = { kind: kind, page: location.pathname.replace(/^\//, ""),
      title: document.title, items: collect() };
    fetch("/submit", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (res) {
        var send = window.parent && window.parent !== window && window.parent.tutorSend;
        return Promise.resolve(send ? send(res.line) : false).then(function (ok) {
          note.textContent = ok ? "Sent — your tutor has it (" + res.path + ")."
            : "Saved to " + res.path + " — the drawer could not take it; tell your tutor to read that file.";
          var report = document.querySelector(".result .report");
          if (report && ok) report.hidden = true;
        });
      })
      .catch(function () {
        note.textContent = "Could not send — is bin/study still running? Tell your tutor by hand.";
        btn.disabled = false;
      });
  });
})();
