<h1>product-component mappings</h1>
<h2>Add a new Mapping</h2>
<form action="/admin/product-component-map/post" method="POST"/>
  <p>
    what's the secret key?
    <input name="secret" />
  </p>
  <p>
    <select name="component_id">
      <option value="0">CHOOSE A COMPONENT</option>
      % for component in components:
        <option value="${component.id}">${component.name}</option>
      % endfor
    </select>
    <select name="product_id">
      <option value="0">CHOOSE A PRODUCT</option>
      % for product in products:
        <option value="${product.id}">${product.name}</option>
      % endfor
    </select>
  </p>
  <input type="submit" />
</form>

<table>
  <tr>
    <td>id</td>
    <td>product id/name</td>
    <td> <--> </td>
    <td>component id/name</td>
  <tr>
  % for mapping in mappings:
  <tr>
    <td>${mapping.id}</td>
    <td>${mapping.product.id}/${mapping.product.name}</td>
    <td> <--> </td>
    <td>${mapping.component.id}/${mapping.component.name}</td>
  </tr>
% endfor
</table>
