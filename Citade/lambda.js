let Swagger = require('swagger-client');

exports.handler = function (event, context, callback) {

    callback(null, { "message": "Successfully executed" });
    Swagger.http({
        url: `https://devapi.currencycloud.com/v2/ibans/find`,
        method: 'get',
        query: { "scope": "all" },
        headers: { "X-Auth-Token": "srtien", "Accept": "application/json" }
    }).then((response) => {
        Swagger.http({
            Swagger.http({
                    url: `https://devapi.currencycloud.com/v2/authenticate/api`,
                    method: 'post',
                    query: {},
                    headers: {"Accept":"application/json","Content-Type":"application/x-www-form-urlencoded"},
                    body: `login_id=ien&api_key=ienien`
                }).then((response) => {
                    // your code goes here
                }).catch((err) => {
                    // error handling goes here
                });
            url: `https://api.sandbox.transferwise.tech/quotes`,
            method: 'post',
            query: {},
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify(response)
        }).then((response) => {
            // your code goes here
        }).catch((err) => {
            // error handling goes here
        });
        // your code goes here
    }).catch((err) => {
        // error handling goes here
    });
}