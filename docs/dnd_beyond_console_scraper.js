function getData() {
  rows = document.querySelectorAll('.info');
  const data = [];
  rows.forEach((row) => {
    const name = row.querySelector('.name .link').innerText;
    const environmentEl = row.querySelector('.monster-environment');
    const environments = (() => {
      const env = environmentEl.querySelector('span');
      if (env && env.hasAttribute('title')) {
        return env.getAttribute('title').split(', ');
      }
      return env.innerText
    })();
    data.push({
      name,
      environments,
    })
  })
  return data;
}