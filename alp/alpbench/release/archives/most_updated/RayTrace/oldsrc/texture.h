/*
 * texture.h This file contains all of the includes and defines for the texture 
 * mapping part of the shader.
 *
 *  $Id: texture.h,v 1.11 2004/02/03 06:00:40 johns Exp $
 */

void InitTextures(void);
color     constant_texture(const vector *, const texture *, const ray *);
color    image_cyl_texture(const vector *, const texture *, const ray *);
color image_sphere_texture(const vector *, const texture *, const ray *);
color  image_plane_texture(const vector *, const texture *, const ray *);
color      checker_texture(const vector *, const texture *, const ray *);
color  cyl_checker_texture(const vector *, const texture *, const ray *);
color         grit_texture(const vector *, const texture *, const ray *);
color         wood_texture(const vector *, const texture *, const ray *);
color       marble_texture(const vector *, const texture *, const ray *);
color       gnoise_texture(const vector *, const texture *, const ray *);
int Noise(flt, flt, flt);
void InitTextures(void);

