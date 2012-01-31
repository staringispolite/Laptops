<h1>Component Types</h1>
<h2>Add a new Component Type</h2>
<form action="/admin/component-type/post" method="POST" />
  <p>
    what's the secret key? <input name="secret" />
  </p>
  <p>
    Name: <input name="name"/>
    Description: <input name="description"/>
    <input type="submit" />
  </p>
</form>

<h2>All Current Component Types</h2>
<table>
  <tr>
    <td>id</td>
    <td>name</td>
    <td>description</td>
  <tr>
% for component_type in component_types:
  <tr>
    <td>${component_type.id}</td>
    <td>${component_type.name}</td>
    <td>${component_type.description}</td>
  </tr>
% endfor
</table>

