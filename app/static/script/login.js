authorization_btn.addEventListener('click', function(event) {
        event.preventDefault();        
        form.style.display = 'block';
        form2.style.display = 'none';
});

registration_btn.addEventListener('click', function(event) {
        event.preventDefault(); 
        form2.style.display = 'block';
        form.style.display = 'none';
});

var form = document.feedback;
var form2 = document.feedback2
form.bsubmit.disabled = true;
form2.bbsubmit.disabled = true;
var information_auth = [form.email, form.password]
information_auth.forEach(input => {
    input.addEventListener("input", () => {
        if (information_auth[0].value === '' || information_auth[1].value === '') {
            form.bsubmit.disabled = true;
        } else {
            form.bsubmit.disabled = false;
        }
    });
});
patterns = []
for (var i = 0; i < information_auth.length; i++){
    patterns.push(new RegExp(information_auth[i].pattern));
}
form.bsubmit.addEventListener("click", function(){
    if (patterns[0].test(information_auth[0].value) && patterns[1].test(information_auth[1].value)){
        console.log(information_auth.reduce((obj,field) => {obj[field.name] = field.value; return obj }, {}),)
    };
}, true);
var information_reg = [form2.reg_login, form2.reg_email, form2.reg_password]
information_reg.forEach(el=>{
    el.addEventListener("input",()=>{
    if (information_reg[0].value === '' || information_reg[1].value === '' || information_reg[2].value === '')
        form2.bbsubmit.disabled = true;
    else
        form2.bbsubmit.disabled = false; 
    });
});
patterns = []
for (var i = 0; i < information_reg.length; i++){
    patterns.push(new RegExp(information_reg[i].pattern));
}
form2.bbsubmit.addEventListener("click", function(){
    if (patterns[0].test(information_reg[0].value) && patterns[1].test(information_reg[1].value) && patterns[2].test(information_reg[2].value)){
        console.log(information_reg.reduce((obj,field) => { obj[field.name] = field.value; return obj }, {}),)
    };
}, true);


