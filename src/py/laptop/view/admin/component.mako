<h1>Components</h1>
<h2>Add a new Component</h2>
<form action="/admin/component/post" method="POST"/>
  <p>
    what's the secret key?
    <input name="secret" />
  </p>
  <p>
    <select name="component_type_id">
      <option value="0">CHOOSE A COMPONENT TYPE</option>
      % for component_type in component_types:
        <option value="${component_type.id}">${component_type.name}</option>
      % endfor
    </select>
    Value: <input name="value"/>
    Name: <input name="name"/>
    Description: <input name="description"/>
  </p>
  <input type="submit" />
</form>

<h2>All Current Components</h2>
<table>
  <tr>
    <td>id</td>
    <td>component_type id</td>
    <td>value</td>
    <td>name</td>
    <td>description</td>
  <tr>
  % for component in components:
  <tr>
    <td>${component.id}</td>
    <td>${component.component_type_id}</td>
    <td>${component.value}</td>
    <td>${component.name}</td>
    <td>${component.description}</td>
  </tr>
% endfor
</table>
