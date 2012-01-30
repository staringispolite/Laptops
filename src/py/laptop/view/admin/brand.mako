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
% for brand in brands:
  <p>
    ${brand.id} ${brand.name} ${brand.description} ${brand.reliability_score} ${brand.url}
  </p>
% endfor

