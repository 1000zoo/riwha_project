const timeOut = setTimeout(() => {
    console.log('1.5초 후 실행');
}, 1500);

const interval = setInterval(() => {
    console.log('1초마다 실행');
}, 1000);

const timeOut2 = setTimeout(() => {
    console.log('실행되지 않습니다.');
}, 3000);

setTimeout(() => {
    clearTimeout((timeOut2));
    clearInterval(interval);
}, 2500);

const immediate1 = setImm(() => {
    console.log('즉시 실행');
});

const immediate1 = (() => {
    console.log('실행 X');
});

clearImmediate(immediate1);