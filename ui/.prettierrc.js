module.exports = {
  printWidth: 150,
  singleQuote: false,
  importOrder: [
    // external dependencies at the top
    "^[.].*(?<!css)$", // local dependencies (except css)
    "^[.].*css$", // local CSS files
  ],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
};
