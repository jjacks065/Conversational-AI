<template>
  <div class="container">
    <header class="card header">
      <h1>JSON Markdown Viewer - Vue</h1>
      <p>Paste your JSON response to render the markdown content below.</p>
    </header>
    <JsonMarkdownViewer />
  </div>
</template>

<script>
import JsonMarkdownViewer from './components/JsonMarkdownViewer.vue'

export default {
  name: 'App',
  components: {
    JsonMarkdownViewer
  }
}
</script>

<style scoped>
.header {
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header h1 {
  margin: 0 0 10px 0;
  font-size: 2.5rem;
}

.header p {
  margin: 0;
  opacity: 0.9;
}
</style>