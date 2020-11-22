"use strict";

window.chartColors = {
  red: "rgb(255, 99, 132)",
  orange: "rgb(255, 159, 64)",
  yellow: "rgb(255, 205, 86)",
  green: "rgb(75, 192, 192)",
  blue: "rgb(54, 162, 235)",
  purple: "rgb(153, 102, 255)",
  grey: "rgb(201, 203, 207)",
};

(function (global) {
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

  var COLORS = ["#4dc9f6", "#f67019", "#f53794", "#537bc4", "#acc236", "#166a8f", "#00a950", "#58595b", "#8549ba"];

  var Samples = global.Samples || (global.Samples = {});
  var Color = global.Color;

  Samples.utils = {
    // Adapted from http://indiegamr.com/generate-repeatable-random-numbers-in-js/
    srand: function (seed) {
      this._seed = seed;
    },

    rand: function (min, max) {
      var seed = this._seed;
      min = min === undefined ? 0 : min;
      max = max === undefined ? 1 : max;
      this._seed = (seed * 9301 + 49297) % 233280;
      return min + (this._seed / 233280) * (max - min);
    },

    numbers: function (config) {
      var cfg = config || {};
      var min = cfg.min || 0;
      var max = cfg.max || 1;
      var from = cfg.from || [];
      var count = cfg.count || 8;
      var decimals = cfg.decimals || 8;
      var continuity = cfg.continuity || 1;
      var dfactor = Math.pow(10, decimals) || 0;
      var data = [];
      var i, value;

      for (i = 0; i < count; ++i) {
        value = (from[i] || 0) + this.rand(min, max);
        if (this.rand() <= continuity) {
          data.push(Math.round(dfactor * value) / dfactor);
        } else {
          data.push(null);
        }
      }

      return data;
    },

    labels: function (config) {
      var cfg = config || {};
      var min = cfg.min || 0;
      var max = cfg.max || 100;
      var count = cfg.count || 8;
      var step = (max - min) / count;
      var decimals = cfg.decimals || 8;
      var dfactor = Math.pow(10, decimals) || 0;
      var prefix = cfg.prefix || "";
      var values = [];
      var i;

      for (i = min; i < max; i += step) {
        values.push(prefix + Math.round(dfactor * i) / dfactor);
      }

      return values;
    },

    months: function (config) {
      var cfg = config || {};
      var count = cfg.count || 12;
      var section = cfg.section;
      var values = [];
      var i, value;

      for (i = 0; i < count; ++i) {
        value = MONTHS[Math.ceil(i) % 12];
        values.push(value.substring(0, section));
      }

      return values;
    },

    color: function (index) {
      return COLORS[index % COLORS.length];
    },

    transparentize: function (color, opacity) {
      var alpha = opacity === undefined ? 0.5 : 1 - opacity;
      return Color(color).alpha(alpha).rgbString();
    },
  };

  // DEPRECATED
  window.randomScalingFactor = function () {
    return Math.round(Samples.utils.rand(-100, 100));
  };

  // INITIALIZATION

  Samples.utils.srand(Date.now());
  /* eslint-enable */
})(this);

function createConfig(position) {
  return {
    type: "line",
    data: {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
        {
          label: "Movie Wishlist Activity",
          borderColor: window.chartColors.red,
          backgroundColor: window.chartColors.red,
          data: [10, 30, 46, 2, 8, 50, 0],
          fill: false,
        },
        {
          label: "User Review Activity",
          borderColor: window.chartColors.blue,
          backgroundColor: window.chartColors.blue,
          data: [7, 49, 46, 13, 25, 30, 22],
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      legend: {
        labels: {
          fontColor: "white",
        },
      },
      title: {
        display: true,
        text: "User Activity Overview",
        fontColor: "#FFFFFF",
        fontSize: 15,
      },
      tooltips: {
        position: position,
        mode: "index",
        intersect: false,
      },
      scales: {
        xAxes: [
          {
            display: true,
            gridLines: {
              display: true,
              color: "#7f8c8d",
            },
          },
        ],
        yAxes: [
          {
            display: true,
            gridLines: {
              display: true,
              color: "#7f8c8d",
            },
          },
        ],
      },
    },
  };
}

window.onload = function () {
  var container = document.querySelector(".canvas-container");

  ["average"].forEach(function (position) {
    var div = document.createElement("div");

    var canvas = document.createElement("canvas");
    container.appendChild(canvas);

    var ctx = canvas.getContext("2d");
    var config = createConfig(position);
    new Chart(ctx, config);
  });
};
