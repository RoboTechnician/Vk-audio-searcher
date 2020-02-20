var stream = new Stream("buff", "rw");
var t = [];
var i = "0"
while ((i = stream.readln()) != "")
	t.push(i);

n = {
            v: function(t) {
                return t.split("").reverse().join("")
            },
            r: function(t, e) {
                var i;
                t = t.split("");
                for (var n = r + r, o = t.length; o--; )
                    ~(i = n.indexOf(t[o])) && (t[o] = n.substr(i - e, 1));
                return t.join("")
            },
            s: function(t, e) {
                var i = t.length;
                if (i) {
                    var r = function(t, e) {
                        var i = t.length
                          , r = [];
                        if (i) {
                            var n = i;
                            for (e = Math.abs(e); n--; )
                                e = (i * (n + 1) ^ e + n) % i,
                                r[n] = e
                        }
                        return r
                    }(t, e)
                      , n = 0;
                    for (t = t.split(""); ++n < i; )
                        t[n] = t.splice(r[i - 1 - n], 1, t[n])[0];
                    t = t.join("")
                }
                return t
            },
            i: function(t, e) {
                return n.s(t, e ^ 80231675)
            },
            x: function(t, e) {
                var i = [];
                return e = e.charCodeAt(0),
                each(t.split(""), function(t, r) {
                    i.push(String.fromCharCode(r.charCodeAt(0) ^ e))
                }),
                i.join("")
            }
        };

function s(t) {
            var r = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/=";
            if (!t || t.length % 4 == 1)
                return !1;
            for (var e, i, n = 0, o = 0, s = ""; i = t.charAt(o++); )
                ~(i = r.indexOf(i)) && (e = n % 4 ? 64 * e + i : i,
                n++ % 4) && (s += String.fromCharCode(255 & e >> (-2 * n & 6)));
            return s
        }

function o(t) {
                var e, i, r = t.split("?extra=")[1].split("#"), o = "" === r[1] ? "" : s(r[1]);
                if (r = s(r[0]),
                "string" != typeof o || !r)
                    return t;
                for (var a = (o = o ? o.split(String.fromCharCode(9)) : []).length; a--; ) {
                    if (e = (i = o[a].split(String.fromCharCode(11))).splice(0, 1, r)[0],
                    !n[e])
                        return t;
                    r = n[e].apply(null, i)
                }
                if (r && "http" === r.substr(0, 4))
                    return r

            return t
        }

stream.rewind();
stream.setEndOfFile(0)
t.forEach(function(item, i, arr) {
	stream.writeln(o(item));
})
stream.close();
