# Sentinel2
### What is the Sentinel-2
[Sentinel-2] is a mission developed by the ESA (Europe Space Agency) on the [Copernicus Programme].
This missions is based on 2 satellites that gather images of the Earth's surface to monitor the land and water.

Each image consists of differents bands that represent differents light wavelengths.
This is information can be accessed through a public API and use it for various purposes.

### What does the project do
1. It first starts by retrieving areas of interest from a database. An area of interest is a polygon based on the surface of the Earth, in other words, a piece of land or water.

2. Then starts a connection with the Sentinel-2 API and queries for images that contain the area of interest. It also queries for images taken in the last 20 days and sets the order to receive first data with smaller size and with less percentage of clouds.

3. After downloading the data, it is extracted and stored in directories identified by the area of interest id. The data contains various bands representing data from differents bandwidths. The bands the program will use (red, green, blue, infrarred and [TCI]) are converted to a useful format from *jp2* to *tif*.

4. The next step creates a shapefile envelope based on the area of interest. The shapefile envelope is the smallest rectangle that covers an area of interest. Even thought the clipped image will contain some data that doesn't belong to the area of interest, this squared shape is preferred so that the image has the edges as smooth as possible.

5. Once created the shapefile envelope, the desired bands are clipped to it, so that they only cover the area of interest.

6. The last step uses the red and infrared band to calculate the [NDVI] (Normalized Difference Vegetation Index), an indicator of vegetation quantity.

### Summary
From an area of interest, we can get satellite images clipped to only cover that area, and also calculate its [NDVI]. All the result images are stored in a *clipped_images* folder.

### To do
As an obvious next step, the program should upload the result images to a database, but the functionality was never completed.

[Sentinel-2]: <https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2>
[Copernicus Programme]: <https://www.copernicus.eu/en>
[TCI]: <https://sentinel.esa.int/web/sentinel/user-guides/sentinel-2-msi/definitions>
[NDVI]: <https://gisgeography.com/ndvi-normalized-difference-vegetation-index/>