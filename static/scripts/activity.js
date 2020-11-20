$(document).ready(() => {
  const x_axis = 53;
  const y_axis = 7;
  const grid = [...new Array(x_axis)].map(() => [...new Array(y_axis)].map(() => 0));

  getDate = (offset) => {
    timeDiff = offset * (3600 * 1000 * 24);
    return new Date(Date.now() + timeDiff).toJSON().slice(0, 10).replace(/-/g, "-");
  };

  grid.map((x, x_index, x_array) => {
    var activityTemp = $(`<g transform="translate(${x_index * 16}, 0)"></g>`);

    x.map((y, y_index, y_array) => {
      var length = x_array.length * y_array.length - 1;
      var reverse_yindex = y_array.length * x_index + y_index - length; // Calculation to display date in reverse
      var get_date = getDate(reverse_yindex);

      var rect = `
        <rect class="day" 
        width="11" 
        height="11" 
        x="15" 
        title="No activity on ${get_date}"
        y="${y_index * 15}" 
        fill="var(--color-activity-nofill)" 
        data-count="0" 
        data-date=${get_date}></rect>
      `;

      activityTemp.append(rect);
    });

    $("#activity-svg").append(activityTemp);
  });

  $("#activity-svg").html($("#activity-svg").html()); // Refresh page to render SVG elements

  // Add event listener to all rect objects
  $(".day").tooltip({ container: "body" });

  console.log($(".day"));

  // Add fill to specific date
  document.querySelectorAll("[data-date='2019-11-28']").forEach((e) => {
    e.setAttribute("fill", "var(--color-activity-fill)");
    e.setAttribute("data-original-title", `Some activities on ${e.getAttribute("data-date")}`);
  });
});
