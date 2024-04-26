function createVersionLink(version) {
  var tag = document.createElement("li");
  var link = document.createElement("a");
  link.setAttribute("class", "dropdown-item");
  // link.setAttribute("href", "/versioned/" + version.link + "/");
  link.setAttribute("rel", "");
  link.setAttribute("target", "");
  link.addEventListener("click", function() { versionClick(version.link) });
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
  // link.setAttribute("href", "/");
  link.setAttribute("rel", "");
  link.setAttribute("target", "");
  link.addEventListener("click", function() { versionClick("") });
  tag.appendChild(link);
  var span = document.createElement("span");
  span.setAttribute("class", "dropdown-text");
  link.appendChild(span);
  span.innerHTML = "Latest";
  return tag;
}

function versionClick(version) {
  // console.log("versionClick " + version);
  var url = window.location.pathname;
  var urlParts = url.split("/");
  console.log(urlParts);
  if (urlParts.length > 2 && urlParts[1] == "versioned") {
    // console.log("versioned " + url);
    urlParts.splice(1, 2);
  } else {
    // console.log("not versioned " + url);
  }

  var newUrl;
  var fallbackUrl;
  if (version == "") {
    newUrl = urlParts.join("/");
    fallbackUrl = "/";
  } else {
    newUrl = "/versioned/" + version + urlParts.join("/");
    fallbackUrl = "/versioned/" + version + "/";
  }
  // console.log("newUrl " + newUrl);
  // console.log("fallbackUrl " + fallbackUrl);

  // Prefetch the new URL and redirect if it exists
  // Otherwise, redirect to the fallback URL
  fetch (newUrl)
    .then((response) => {
      // console.log("response");
      // console.log(response);
      if (response.ok) {
        window.location.href = newUrl;
      } else {
        window.location.href = fallbackUrl;
      }
    });
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
