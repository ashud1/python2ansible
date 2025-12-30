// "use strict";

function fileUpload() {
  const fileInput = document.getElementById("fbox");
  const ibox = document.getElementById("ibox");
  const obox = document.getElementById("obox");

  //   console.log(fileInput);
  const file = fileInput.files[0];
  //   ibox.value = "";

  if (!file) {
    console.log("please select file");
    alert("please select file");
  } else {
    // console.log(file.name);
    // ibox.value = "uploaded file content";
    ibox.value = "";
    obox.value = "";
    file
      .text()
      .then((text) => {
        ibox.value = text;
      })
      .catch((err) => {
        console.error(err);
      });
  }
  fileInput.value = "";
}

// let j = 0;

function addParam() {
  j++;
  const textArea = document.getElementById("paraArea");
  const input = document.createElement("input");
  const div = document.createElement("div");
  input.type = "text";
  input.placeholder = "Added parameter name";
  input.className = "dynamic-textbox";
  input.name = "dynamic-textbox-Para" + j;
  input.id = "dynamic-textbox-ParaJs" + j;

  const value = document.createElement("input");
  value.type = "text";
  value.placeholder = "Added value";
  value.className = "dynamic-textbox";
  value.name = "dynamic-textbox-Value" + j;
  value.id = "dynamic-textbox-ValueJs" + j;

  const lable = document.createElement("label");
  lable.textContent = "param " + j + " : ";
  lable.name = "param";
  lable.htmlFor = "dynamic-textbox-ParaJs" + j;

  div.appendChild(lable);
  div.appendChild(input);
  div.appendChild(value);

  textArea.appendChild(div);
}
