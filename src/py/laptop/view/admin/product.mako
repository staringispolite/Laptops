<h1>products</h1>
<h2>Add a new Product</h2>
<form action="/admin/product/post" method="POST"/>
  <p>
    what's the secret key?
    <input name="secret" />
  </p>
  <p>
    <select name="brand_id">
      <option value="0">CHOOSE A BRAND</option>
      % for brand in brands:
        <option value="${brand.id}">${brand.name}</option>
      % endfor
    </select>
    <select name="type">
      <option name="">CHOOSE A TYPE</option>
      <option name="desktop">desktop</option>
      <option name="laptop">laptop</option>
      <option name="tablet">tablet</option>
    </select>
    Name: <input name="name"/>
  </p>
  <input type="submit" />
</form>

<h2>All Current Products</h2>
<table>
  <tr>
    <td>id</td>
    <td>name</td>
    <td>type</td>
    <td>brand id</td>
  <tr>
  % for product in products:
  <tr>
    <td>${product.id}</td>
    <td>${product.name}</td>
    <td>${product.type}</td>
    <td>${product.brand_id}</td>
  </tr>
% endfor
</table>
