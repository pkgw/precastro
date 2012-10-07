%module precastro

%{
#include "novas.h"
#include "sofa.h"
%}

/* NOVAS */

%rename (novas_cat_entry) cat_entry;

typedef struct {
    char starname[SIZE_OF_OBJ_NAME];
    char catalog[SIZE_OF_CAT_NAME];
    long int starnumber;
    double ra;
    double dec;
    double promora;
    double promodec;
    double parallax;
    double radialvelocity;
} cat_entry;

%rename (novas_object) object;

typedef struct {
    short int type;
    short int number;
    char name[SIZE_OF_OBJ_NAME];
    cat_entry star;
} object;

%rename (novas_on_surface) on_surface;

typedef struct {
    double latitude;
    double longitude;
    double height;
    double temperature;
    double pressure;
} on_surface;

%rename (novas_in_space) in_space;

typedef struct {
    double sc_pos[3];
    double sc_vel[3];
} in_space;

%rename (novas_observer) observer;

typedef struct {
    short int where;
    on_surface on_surf;
    in_space near_earth;
} observer;

short int astro_star (double jd_tt, cat_entry *star, short int accuracy,
		      double *OUTPUT, double *OUTPUT);
