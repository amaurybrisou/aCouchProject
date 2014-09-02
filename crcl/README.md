Country/Regions/Cities/Languages Zato Module

39446 cities,
275 countries,
100 languages,
3953 regions
and 208 relations between countries and languages

### Deploy (standalone):

[Base module](../commons/base.py)

Create a database called and an SQL outgoing connection called 'crcl'.

I usualy deploy the services in countries.py and crcl_init.py as this :

* crcl Drop Database																				/crcl/drop								crcl-init.drop								GET
* crcl Generate Database																		/crcl/generate						crcl-init.generate						GET
* crcl Get Countries																				/crcl/countries						crcl-countries.get-countries						GET
* crcl Get Country By countryId or countryName							/crcl/country							crcl-countries.get-country							GET
* crcl Get Country Cities by countryId or countryName				/crcl/country/cities			crcl-countries.get-country-cities			GET
* crcl Get Country Languages by countryId or countryName		/crcl/country/languages		crcl-countries.get-country-languages		GET
* crcl Get Country Regions by countryId or countryName			/crcl/country/regions			crcl-countries.get-country-regions	  	GET

### Usage :
	Just read the tests

### Tests:

You can run tests with Postman chrome extension, importing the collections in tests/postman