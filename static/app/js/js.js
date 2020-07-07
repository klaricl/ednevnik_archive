let semesterNumber = document.getElementById("semesterNumber").firstChild.data;
let firstSemester = document.getElementById("firstSemester");
let secondSemester = document.getElementById("secondSemester");
let firstSemesterTab = document.getElementById("firstSemesterTab");
let secondSemesterTab = document.getElementById("secondSemesterTab");

if (semesterNumber == "1") {
  firstSemester.classList.add("active");
  firstSemesterTab.classList.add("active");
  secondSemesterTab.classList.remove("active");
  secondSemester.classList.remove("active");
} else {
  firstSemester.classList.remove("active");
  firstSemesterTab.classList.remove("active");
  secondSemesterTab.classList.add("active");
  secondSemester.classList.add("active");
}



