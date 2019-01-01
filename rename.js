const exec = require("child_process").exec;
// const spawn = require("child_process").spawn;
const fs = require("fs");

const path = "static/images/" + process.argv[2];

const catchERR = err => {
  if (err) {
    console.error(err);
    return;
  }
};

const puts = (err, stdout, stderr) => {
  catchERR(err);
  let ls = stdout.split("\n");
  ls = ls.slice(0, ls.length - 1);
  // 10枚以上100枚未満かつ、全てjpgのみ対応
  if (ls.length >= 10) {
    for (let i = 1; i < 10; i++) {
      fs.rename(
        `${path + "/" + ls[i - 1]}`,
        `${path + "/image0" + i + ".jpg"}`,
        catchERR
      );
    }
    for (let i = 10; i <= ls.length; i++) {
      fs.rename(
        `${path + "/" + ls[i - 1]}`,
        `${path + "/image" + i + ".jpg"}`,
        catchERR
      );
    }
  }
  console.log(ls.length);
};

// console.log(path);

const command = `cd ${path} && ls`;
exec(`${command}`, puts);

// // これでやっと、pythonからの標準出力が取得できる
// const main = spawn("python", ["main.py"]);
// main.stdout.on("data", data => {
//   console.log(`stdout: ${data}`);
// });

(() => {
  console.log(process.argv);
})();
