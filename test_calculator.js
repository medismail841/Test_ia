const assert = require("assert");
const Calculator = require("./static/calculator.js");

let passed = 0;
let failed = 0;

function check(label, fn) {
  try {
    fn();
    passed++;
    console.log("PASS " + label);
  } catch (err) {
    failed++;
    console.log("FAIL " + label + " -> " + err.message);
  }
}

function evalOk(expression, expected) {
  check(`evaluate("${expression}") === ${expected}`, function () {
    const actual = Calculator.evaluate(expression);
    assert.strictEqual(actual, expected);
  });
}

function evalThrows(expression) {
  check(`evaluate("${expression}") throws`, function () {
    assert.throws(function () {
      Calculator.evaluate(expression);
    });
  });
}

evalOk("42", 42);
evalOk("1+2", 3);
evalOk("1+2+3", 6);
evalOk("2*3+4", 10);
evalOk("3+4*2", 11);
evalOk("10-4/2", 8);
evalOk("5/2", 2.5);
evalOk("7-2-1", 4);
evalOk("2.5*4", 10);
evalOk("8/2/2", 2);
evalOk("0*999", 0);
evalOk("100/5+6", 26);

evalThrows("");
evalThrows("abc");
evalThrows("6/0");
evalThrows("1+");
evalThrows("1**2");
evalThrows("1 2");

check('formatResult(0.1 + 0.2) === "0.3"', function () {
  assert.strictEqual(Calculator.formatResult(0.1 + 0.2), "0.3");
});

check('formatResult(1 / 3) is a string', function () {
  assert.strictEqual(typeof Calculator.formatResult(1 / 3), "string");
});

console.log("\n" + passed + " passed, " + failed + " failed");
process.exit(failed === 0 ? 0 : 1);