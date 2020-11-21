let date_list = [];

// Function to get all activity date
getActivityDate = (date) => {
  date_list = date;
};

$(document).ready(() => {
  const x_axis = 53;
  const y_axis = 7;
  const grid = [...new Array(x_axis)].map(() => [...new Array(y_axis)].map(() => 0));

  // Function to get date
  getDate = (offset) => {
    timeDiff = offset * (3600 * 1000 * 24);
    return new Date(Date.now() + timeDiff).toJSON().slice(0, 10).replace(/-/g, "-");
  };

  dateFormat = (date) => new Date(date).toJSON().slice(0, 10).replace(/-/g, "-");

  // User activity tracker grid
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

  // Add fill to specific date
  date_list.map((dl) => {
    const dd = dateFormat(dl[1]);

    document.querySelector(`[data-date='${dd}']`).setAttribute("fill", "var(--color-activity-fill)");
    document.querySelector(`[data-date='${dd}']`).setAttribute("data-original-title", `${dl[0]} activities on ${dd}`);
  });

  // Make description editable
  document.querySelector("#profile-editable").onclick = () => {
    document.querySelector("#profile-editable p").setAttribute("class", "iseditable");
    document.querySelector("#profile-editable p").contentEditable = true;
    document.querySelector("#save-profile-button").style.display = "block";
  };

  // Disable styles when done editing profile details
  document.querySelector("#save-profile-button").onclick = () => {
    var desc_text = document.querySelector("#profile-editable p").textContent;

    const http = new XMLHttpRequest();
    const url = "/profile";
    http.open("POST", url);
    http.send(desc_text);

    document.querySelector("#profile-editable p").removeAttribute("class");
    document.querySelector("#profile-editable p").contentEditable = false;
    document.querySelector("#save-profile-button").style.display = "none";
  };
});
