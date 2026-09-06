(function (root, factory) {
  if (typeof module === "object" && typeof module.exports === "object") {
    module.exports = factory();
  } else {
    root.Calculator = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  function tokenize(input) {
    if (typeof input !== "string" || input.trim() === "") {
      throw new Error("Empty expression");
    }
    const tokens = [];
    const re = /(\d+(?:\.\d+)?)|([+\-*\/])|\s+|(.+)/g;
    let m;
    while ((m = re.exec(input)) !== null) {
      if (m[1]) {
        tokens.push({ type: "number", value: parseFloat(m[1]) });
      } else if (m[2]) {
        tokens.push({ type: "op", value: m[2] });
      } else if (!m[3]) {
        continue;
      } else {
        throw new Error("Invalid character in expression: " + m[3]);
      }
    }
    return tokens;
  }

  function evaluate(expression) {
    const tokens = tokenize(expression);
    if (tokens.length === 1 && tokens[0].type === "number") {
      return tokens[0].value;
    }
    if (tokens.length < 3 || tokens.length % 2 === 0) {
      throw new Error("Invalid expression");
    }
    for (let i = 0; i < tokens.length; i++) {
      const isNumber = i % 2 === 0;
      if (isNumber && tokens[i].type !== "number") {
        throw new Error("Invalid expression");
      }
      if (!isNumber && tokens[i].type !== "op") {
        throw new Error("Invalid expression");
      }
    }

    let current = tokens[0].value;
    const terms = [];
    const additiveOps = [];
    for (let i = 1; i < tokens.length; i += 2) {
      const op = tokens[i].value;
      const num = tokens[i + 1].value;
      if (op === "*") {
        current *= num;
      } else if (op === "/") {
        if (num === 0) throw new Error("Division by zero");
        current /= num;
      } else {
        terms.push(current);
        additiveOps.push(op);
        current = num;
      }
    }
    terms.push(current);

    let result = terms[0];
    for (let i = 0; i < additiveOps.length; i++) {
      result = additiveOps[i] === "+" ? result + terms[i + 1] : result - terms[i + 1];
    }
    return result;
  }

  function formatResult(value) {
    if (typeof value !== "number" || !isFinite(value)) {
      throw new Error("Invalid result");
    }
    const rounded = Number(value.toPrecision(12));
    return String(rounded);
  }

  return { evaluate: evaluate, formatResult: formatResult };
});