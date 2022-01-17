const {odd, even} = require('./var'); //속성명과 변수명이 똑같아야 한다.
const checkNumber = require('./func'); //변수명은 아무거나 해도 된다.

function checkStringOddorEven(str) {
    if(str.length % 2) {
        return odd;
    } else{
        return even;
    }
}

console.log(checkNumber(10));
console.log(checkStringOddorEven('hello'));