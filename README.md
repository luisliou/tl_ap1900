TP-Link AP1900GI Auto Login and Retrieve Infomation

Original Login JavaScript:

        function r(e, t, i) {
        for (var n = "", a = 187, s = 187, l = e.length, d = t.length, o = Math.max(l, d), r = i.length, c = 0; c < o; c++)
            a = 187,
            s = 187,
            c >= l ? s = t.charCodeAt(c) : c >= d ? a = e.charCodeAt(c) : (a = e.charCodeAt(c),
            s = t.charCodeAt(c)),
            n += i.charAt((a ^ s) % r);
        return n
    }
    function c(e) {
        return r(e, "RDpbLfCPsJZ7fiv", "yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW")
    }
    
        auth: function(t, a, s) {
            function l() {
                var e = n(t + ";" + c(a));
                m.token = r(m.authData.pwd, e, m.authData.dic),
                v.send(v.TDDP_AUTH, "", s)
            }
            i.set("id", ""),
            v.token(""),
            v.read(0, e.noop, function() {
                e.delay(l)
            })
        },

