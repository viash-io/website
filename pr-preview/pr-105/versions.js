function createVersionLink(version, json) {
  var tag = document.createElement("li");
  var link = document.createElement("a");
  link.setAttribute("class", "dropdown-item");
  link.setAttribute("rel", "");
  link.setAttribute("target", "");
  link.addEventListener("click", function() {
    versionClick(versionLink(version, json))
  });
  tag.appendChild(link);
  var span = document.createElement("span");
  span.setAttribute("class", "dropdown-text");
  link.appendChild(span);
  span.innerHTML = versionName(version, json);
  return tag;
}

function versionName(version, json) {
  if (version.name) {
    return version.name;
  }
  var name = "Viash " + version.version;
  if (version.version === json["latest"]) {
    name += " (latest)";
  }
  return name;
}

function versionLink(version, json) {
  if (version.link) {
    return version.link;
  }
  if (version.version === json["latest"]) {
    return "";
  }
  return version.version;
}

function versionClick(version) {
  var url = window.location.pathname;
  var urlParts = url.split("/");
  console.log(urlParts);
  if (urlParts.length > 2 && urlParts[1] === "versioned") {
    urlParts.splice(1, 2);
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
  for (var i = 0; i < json.versions.length; i++) {
    var version = json.versions[i];
    list.appendChild( createVersionLink(version, json) );
  }

  // Alter the navbar logo link to point to the root
  var navbarElements = document.getElementsByClassName("navbar-brand");
  navbarElements[0].setAttribute("href", "/");

  // Alter the version dropdown to show the displayed version
  var url = window.location.pathname;
  var urlParts = url.split("/");
  const versionPath = urlParts.length > 3 && urlParts[1] === "versioned" ? urlParts[2] : "";
  for (var i = 0; i < json.versions.length; i++) {
    const version = json.versions[i];
    const versionLink = versionLink(version, json);
    if (link === versionPath) {
      const dropdownElement = document.getElementById("nav-menu-version");
      const versionName = versionName(version, json);
      dropdownElement.innerHTML = versionName;
      break;
    }
  }
}

fetch('/versions.json')
    .then((response) => response.json())
    .then((json) => setVersionLinks(json));
