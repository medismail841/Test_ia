(function () {
  "use strict";

  const AUTH_VIEW = document.getElementById("auth-view");
  const CALC_VIEW = document.getElementById("calc-view");
  const AUTH_ERROR = document.getElementById("auth-error");
  const LOGIN_FORM = document.getElementById("login-form");
  const REGISTER_FORM = document.getElementById("register-form");
  const TAB_LOGIN = document.getElementById("tab-login");
  const TAB_REGISTER = document.getElementById("tab-register");
  const LOGOUT_BTN = document.getElementById("logout-btn");
  const CALC_USERNAME = document.getElementById("calc-username");
  const DISPLAY = document.getElementById("calc-display");
  const CALC_ERROR = document.getElementById("calc-error");

  let expression = "";

  function showAuthView() {
    AUTH_VIEW.hidden = false;
    CALC_VIEW.hidden = true;
  }

  function showCalcView(username) {
    CALC_USERNAME.textContent = username;
    AUTH_VIEW.hidden = true;
    CALC_VIEW.hidden = false;
  }

  function showAuthError(message) {
    AUTH_ERROR.textContent = message;
    AUTH_ERROR.hidden = false;
  }

  function clearAuthError() {
    AUTH_ERROR.hidden = true;
  }

  function setTab(active) {
    const isLogin = active === "login";
    TAB_LOGIN.classList.toggle("active", isLogin);
    TAB_REGISTER.classList.toggle("active", !isLogin);
    LOGIN_FORM.hidden = !isLogin;
    REGISTER_FORM.hidden = isLogin;
  }

  function displayText() {
    DISPLAY.textContent = expression === "" ? "0" : expression;
  }

  function showCalcError(message) {
    CALC_ERROR.textContent = message;
    CALC_ERROR.hidden = false;
  }

  function hideCalcError() {
    CALC_ERROR.hidden = true;
  }

  function appendToExpression(ch) {
    expression += ch;
    displayText();
  }

  function insertDigit(digit) {
    hideCalcError();
    if (expression === "0") {
      expression = digit === "." ? "0." : digit;
    } else {
      expression += digit;
    }
    displayText();
  }

  function insertOperator(op) {
    hideCalcError();
    const last = expression[expression.length - 1];
    if (last && "+-*/".includes(last)) {
      expression = expression.slice(0, -1) + op;
    } else if (expression !== "") {
      expression += op;
    }
    displayText();
  }

  function insertDecimal() {
    hideCalcError();
    if (expression === "") {
      expression = "0.";
      displayText();
      return;
    }
    const parts = expression.split(/[+\-*/]/);
    const current = parts[parts.length - 1];
    if (current.includes(".")) return;
    expression += ".";
    displayText();
  }

  function negate() {
    hideCalcError();
    if (expression === "" || expression === "0") return;
    const parts = expression.split(/[+\-*/]/);
    const current = parts[parts.length - 1];
    if (current === "") return;
    const replacement = current.startsWith("-") ? current.slice(1) : "-" + current;
    expression =
      expression.slice(0, expression.length - current.length) + replacement;
    displayText();
  }

  function clearAll() {
    expression = "";
    hideCalcError();
    displayText();
  }

  function backspace() {
    hideCalcError();
    expression = expression.slice(0, -1);
    displayText();
  }

  function evaluateExpression() {
    hideCalcError();
    try {
      const result = window.Calculator.formatResult(
        window.Calculator.evaluate(expression)
      );
      expression = result;
      displayText();
    } catch (err) {
      expression = "";
      displayText();
      showCalcError(err.message);
    }
  }

  function handleKeyEvent(e) {
    const key = e.key;
    if (/[0-9]/.test(key)) {
      insertDigit(key);
    } else if (key === ".") {
      insertDecimal();
    } else if ("+-*/".includes(key)) {
      insertOperator(key);
    } else if (key === "Enter" || key === "=") {
      e.preventDefault();
      evaluateExpression();
    } else if (key === "Backspace") {
      backspace();
    } else if (key === "Escape") {
      clearAll();
    } else {
      return;
    }
    e.preventDefault();
  }

  async function postJSON(url, body) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.detail || "Request failed.");
    }
    return data;
  }

  async function checkAuth() {
    try {
      const res = await fetch("/auth/check");
      const data = await res.json();
      if (data.authenticated) {
        showCalcView(data.username);
      } else {
        showAuthView();
      }
    } catch (err) {
      showAuthView();
    }
  }

  LOGIN_FORM.addEventListener("submit", async function (e) {
    e.preventDefault();
    clearAuthError();
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value;
    try {
      const data = await postJSON("/login", { username, password });
      showCalcView(data.username);
    } catch (err) {
      showAuthError(err.message);
    }
  });

  REGISTER_FORM.addEventListener("submit", async function (e) {
    e.preventDefault();
    clearAuthError();
    const username = document.getElementById("register-username").value.trim();
    const password = document.getElementById("register-password").value;
    try {
      const data = await postJSON("/register", { username, password });
      showCalcView(data.username);
    } catch (err) {
      showAuthError(err.message);
    }
  });

  TAB_LOGIN.addEventListener("click", function () {
    setTab("login");
  });

  TAB_REGISTER.addEventListener("click", function () {
    setTab("register");
  });

  LOGOUT_BTN.addEventListener("click", async function () {
    try {
      await fetch("/logout", { method: "POST" });
    } finally {
      expression = "";
      displayText();
      setTab("login");
      showAuthView();
    }
  });

  document.querySelectorAll(".key").forEach(function (key) {
    key.addEventListener("click", function () {
      const action = key.dataset.action;
      if (action === "digit") insertDigit(key.dataset.value);
      else if (action === "op") insertOperator(key.dataset.value);
      else if (action === "decimal") insertDecimal();
      else if (action === "negate") negate();
      else if (action === "equals") evaluateExpression();
      else if (action === "clear") clearAll();
      else if (action === "backspace") backspace();
    });
  });

  document.addEventListener("keydown", handleKeyEvent);

  setTab("login");
  checkAuth();
})();