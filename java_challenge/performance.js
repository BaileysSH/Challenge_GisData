let tick;
const times = [];
const start = () => {
  tick = setInterval(function () {
    console.time("Total");
    const n = performance.now();
    process();
    times.push(performance.now() - n);
    console.timeEnd("Total");

    const avg = times.reduce((prev, curr) => prev + curr, 0);
    console.log("Avg ", avg / times.length, " - ", times.length);
    if (times.length > 400) {
      clearInterval(tick);
    }
  }, 100);
};
