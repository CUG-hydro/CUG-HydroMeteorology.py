library(sf)

x = read_sf("data/shp/bou2_4p_ChinaProvince.shp")
x2 <- st_simplify(x, dTolerance = 1e3)
write_sf(x2, "data/shp/bou2_4p_ChinaProvince_sml.shp", overwrite = TRUE)
