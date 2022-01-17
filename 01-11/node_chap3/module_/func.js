//import value  from './var'; //..은 부모 폴더, ...은 조부모, .은 현재 폴더
const {odd, even} = require('./var'); //구조분해할당

function checkOddOrEven(number) {
    if(number % 2){
        return odd;
    } else{
        return even;
    }
}

module.exports = checkOddOrEven;