//파일시스템 접근에 주의해야한다.

console.log(__filename);
console.log(__dirname);

const h = __filename;

console.log(h);

console.log("0" == 0)
console.log([] == 0)
console.log("0" == [])

console.log("0" === 0) //형식까지 같아야한다.