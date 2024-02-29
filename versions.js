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

function addVersionLinks(json) {
  var element = document.getElementById("nav-menu-version");
  var list = element.nextElementSibling;
  list.appendChild( createLatestLink() );
  for (var i = 0; i < json.versions.length; i++) {
    var version = json.versions[i];
    list.appendChild( createVersionLink(version) );
  }
}

fetch('/versions.json')
    .then((response) => response.json())
    .then((json) => addVersionLinks(json));
