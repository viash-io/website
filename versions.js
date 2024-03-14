function createVersionLink(version) {
  var tag = document.createElement("li");
  var link = document.createElement("a");
  link.setAttribute("class", "dropdown-item");
  link.setAttribute("href", "/versioned/" + version.link + "/");
  link.setAttribute("rel", "");
  link.setAttribute("target", "");
  tag.appendChild(link);
  var span = document.createElement("span");
  span.setAttribute("class", "dropdown-text");
  link.appendChild(span);
  span.innerHTML = version.name;
  return tag;
}

function createLatestLink() {
  var tag = document.createElement("li");
  var link = document.createElement("a");
  link.setAttribute("class", "dropdown-item");
  link.setAttribute("href", "/");
  link.setAttribute("rel", "");
  link.setAttribute("target", "");
  tag.appendChild(link);
  var span = document.createElement("span");
  span.setAttribute("class", "dropdown-text");
  link.appendChild(span);
  span.innerHTML = "Latest";
  return tag;
}

function setVersionLinks(json) {
  // Populate the version drowdown
  var dropdownElement = document.getElementById("nav-menu-version");
  var list = dropdownElement.nextElementSibling;
  list.appendChild( createLatestLink() );
  for (var i = 0; i < json.versions.length; i++) {
    var version = json.versions[i];
    list.appendChild( createVersionLink(version) );
  }

  // Alter the navbar logo link to point to the root
  var navbarElements = document.getElementsByClassName("navbar-brand");
  navbarElements[0].setAttribute("href", "/");
}

fetch('/versions.json')
    .then((response) => response.json())
    .then((json) => setVersionLinks(json));
