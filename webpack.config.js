const path = require('path');

module.exports = {
  mode: 'development',
  entry: './static/vue/reload-files.js',
  output: {
    // directory where the output file goes, defined from __dirname where webpack runs (root of project)
    path: path.resolve(__dirname, 'static/dist'),
    filename: 'bundle.js'
  },
  devtool: 'eval-source-map',
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [ // loaders run from last to first in the list
          'style-loader', // adds a <style> tag to index.html?? to link the css
          'css-loader' // collects all css into a big string
        ]
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    }
  }
};

