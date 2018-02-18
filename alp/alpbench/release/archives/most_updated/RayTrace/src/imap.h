/*
 * imap.h - This file contains defines etc for doing image map type things.  
 *
 *  $Id: imap.h,v 1.7 2002/07/09 18:17:25 johns Exp $
 */

void       ResetImage(void);
void       LoadImage(rawimage *);
rawimage * AllocateImage(const char *);
void       DeallocateImage(rawimage *);
void       ResetImages(void);
rawimage * DecimateImage(const rawimage *);
mipmap *   LoadMIPMap(const char *);
mipmap *   CreateMIPMap(const rawimage *);
color      MIPMap(const mipmap *, flt, flt, flt);
color      ImageMap(const rawimage *, flt, flt);
 
