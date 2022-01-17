//this ==  global ?
console.log(this === module.exports)
console.log(this);
function a() {
    console.log(this === global)
}
a();