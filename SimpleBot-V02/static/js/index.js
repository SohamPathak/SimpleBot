var part, emoji, _emo,
  bind = function(fn, args) {
    return function() {
      return fn.apply(args, arguments);
    };
  };
part = (function() {
  function part(x, y, rgba) {
    this.x = x;
    this.y = y;
    this.posX = x;
    this.posY = y;
    this.color = "rgba(" + rgba[0] + ", " + rgba[1] + ", " + rgba[2] + ", " + rgba[3] + ")";
  }

  return part;

})();
var rndCol = function() {
  var r = (~~(Math.random() * 255));
  var g = (~~(Math.random() * 255));
  var b = (~~(Math.random() * 255));

  return 'rgba(' + r + ',' + g + ',' + b + ',' + '1)';
}
emoji = (function() {
  function emoji() {
    this.build = bind(this.build, this);
    this.sel = bind(this.sel, this);
    this.c = document.getElementById("canv");
    this.$$ = this.c.getContext('2d');
    this.arr = [];
    this.$select = $("#emo select");
    this.$select.change(this.sel);
    this.c.width = window.innerWidth / 4;
    this.c.height = window.innerHeight / 4;
  }

  emoji.prototype.toP = function() {
    var data, i, id, res, x, y;
    this.arr = [];
    id = this.$$.getImageData(0, 0, this.c.width, this.c.height);
    data = id.data;
    i = 0;
    x = 0;
    y = 0;
    res = [];
    while (i < data.length) {
      if (!(data[i] === 0 && data[i + 1] === 0 && data[i + 2] === 0)) {
        this.arr.push(new part(x, y, [data[i], data[i + 1], data[i + 2], data[i + 3]]));
      }
      i += 4;
      x += 1;
      if (x > this.c.width - 1) {
        y += 1;
        res.push(x = 0);
      } else {
        res.push(void 0);
      }
    }
    return res;
  };

  emoji.prototype.draw = function(txt) {
    this.$$.clearRect(0, 0, this.c.width, this.c.height);
    this.$$.font = "5em sans-serif";
    this.$$.textAlign = "center";
    this.$$.textBaseline = "middle";
    this.$$.fillStyle = "hsla(0,0%,0%,1)";
    this.$$.fillRect(0, 0, this.c.width, this.c.height);
    this.$$.fillStyle = rndCol();
    this.$$.shadowColor = "hsla(0,0%,10%,1)";
    this.$$.shadowOffsetX = 1;
    this.$$.shadowOffsetY = 1;
    this.$$.shadowBlur = 5;
    this.$$.fillText(txt, this.c.width / 2, this.c.height / 2, this.c.width);
    this.toP();
    return this.goEmo();
  };

  emoji.prototype.goEmo = function() {
    var p, j, _arr, res;
    _arr = this.arr;
    res = [];
    for (var j in _arr) {
      p = _arr[j];
      p.x = Math.floor(Math.random() * this.c.width);
      res.push(p.y = Math.floor(Math.random() * this.c.height));
    }
    return res;
  };

  emoji.prototype.calc = function(a, b) {
    var diff, stat;
    diff = a - b;
    if (diff < 0) {
      diff = diff * -1;
    }
    stat = 1;
    if (diff > 50) {
      stat = 10;
    } else if (diff > 10) {
      stat = 5;
    }
    return stat;
  };

  emoji.prototype.sel = function() {
    var txt;
    txt = this.$select.val();
    if (txt) {
      return this.draw(txt);
    }
  };

  emoji.prototype.build = function() {
    var p, stat, j, _arr, res;
    this.$$.clearRect(0, 0, this.c.width, this.c.height);
    _arr = this.arr;
    res = [];
    for (var j in _arr) {
      p = _arr[j];
      this.$$.fillStyle = p.color;
      this.$$.shadowBlur = 0;
      this.$$.shadowOffsetX = 0;
      this.$$.shadowOffsetY = 0;
      this.$$.fillRect(p.x, p.y, 1, 1);
      if (p.x !== p.posX) {
        stat = this.calc(p.x, p.posX);
        if (p.x > p.posX) {
          p.x -= stat;
        } else {
          p.x += stat;
        }
      }
      if (p.y !== p.posY) {
        stat = this.calc(p.y, p.posY);
        if (p.y > p.posY) {
          res.push(p.y -= stat);
        } else {
          res.push(p.y += stat);
        }
      } else {
        res.push(void 0);
      }
    }
    return res;
  };
  return emoji;

})();

_emo = {};

$(function() {
  _emo = new emoji;
  _emo.draw("👾");
  run();

});

function run() {
  window.requestAnimationFrame(run);
  _emo.build();
}
window.addEventListener('resize', function(){
   this.c.width = window.innerWidth / 4;
   this.c.height = window.innerHeight / 4;
}, false);