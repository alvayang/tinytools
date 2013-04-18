/**
 * @file   ini.h
 * @author alvayang <netyang@gmail.com>
 * @date   Sun Feb 19 10:15:45 2012
 * 
 * @brief  阅读ini文件
 * 
 * 
 */
#ifndef __INI_H__
#define __INI_H__

struct item {
    char *name;
    char *value;
    struct item *next;
};

struct section{
    char *name;
    struct item *items;
    struct section *next;
    
};


#define MAX_LINE 200
#define MAX_SECTION 50
#define MAX_NAME 50

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>

#endif
