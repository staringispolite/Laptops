<h1>brands</h1>
<h2>Add a new Brand</h2>
<form action="/admin/brand/post" method="POST" />
  <p>
    what's the secret key? <input name="secret" />
  </p>
  <p>
    Reliability score: <input name="reliability_score"/>
    Name: <input name="name"/>
    Description: <input name="description"/>
    URL: <input name="url"/>
    <input type="submit" />
  </p>
</form>

<h2>All Current Brands</h2>
<table>
  <tr>
    <td>id</td>
    <td>name</td>
    <td>description</td>
    <td>reliability score</td>
    <td>url</td>
  <tr>
% for brand in brands:
  <tr>
    <td>${brand.id}</td>
    <td>${brand.name}</td>
    <td>${brand.description}</td>
    <td>${brand.reliability_score}</td>
    <td>${brand.url}</td>
  </tr>
% endfor
</table>

