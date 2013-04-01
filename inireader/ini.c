/**
 * @file   ini.c
 * @author alvayang <netyang@gmail.com>
 * @date   Sun Feb 19 10:19:58 2012
 * 
 * @brief  解析ini文件
 * 
 * 
 */


#include "ini.h"



void debug_item(struct item *_item)
{
     printf("[Name]:%s:[Value]:%s\n", _item->name, _item->value);
}

void debug_section(struct section *_sec)
{
     struct section *i = _sec;
    
     while(i)
     {
          printf("[Name]%s\n", i->name);
          if(i->items)
          {
                    
               struct item *item = i->items;
               while(item)
               {
                    debug_item(item);
                    if(item->next)
                    {
                         item = item->next;
                    }
                            
                    else
                         break;
               }
          }
            
            
          if(i->next)
          {
               i = i->next;
          } else
               break;
     }
}

int buf_type(char *buf)
{
     char b = buf[0];
     while(b != '\n')
     {
          if(!isspace(b))
          {
               switch(b)
               {
               case ';':
               {
                    return 1;
               }
               break;
               case '[':
               {
                    return 2;
               }
               break;
               case '=' :
               {
                    return 3;
               }
               break;
               }
          }
          b = *buf++;
     }
     return 0;
}


struct item *parse_item(char *buf)
{
     char c = *buf;
     struct item *item = (struct item *)malloc(sizeof(struct item));
     item->name = (char *)malloc(sizeof(char) * MAX_NAME);
     memset(item->name, 0, sizeof(char) * MAX_NAME);
     item->value = (char *)malloc(sizeof(char) * MAX_NAME);
     memset(item->value, 0, sizeof(char) * MAX_NAME);
    
     int key_area = 0;
     int item_pos = 0;
     int stop_flag = 0;
    
     while(c != '\0')
     {
          switch(c)
          {
          case '=' : 
          {
               key_area = 1;
               item_pos = -1;
          }
          break;
          case ' ':
          {
               item_pos--;
          }
          break;
          case ';':
          {
               stop_flag = 1;
               break;
          }
          break;
          default:
          {
               if(stop_flag == 1) break;
               if(key_area == 0)
               {
                    // key
                    item->name[item_pos] = c;
               }
               else
               {
                    item->value[item_pos] = c;
               }
          }
          }
          item_pos++;
          c = *++buf;
     }
     item->next = NULL;
#if 0
     debug_item(item);
#endif
     return item;
            
}


struct section *parse_section(char *buf)
{
     struct section *ret = (struct section *)malloc(sizeof(struct section));
     ret->name = (char *)malloc(sizeof(char) * MAX_NAME);
     memset(ret->name, 0, MAX_NAME * sizeof(char));
     int _name_index = 0;
     int stop_flag = 0;
     char c = *buf;
     /* printf("Section buf:[%s]\n", buf); */
     while(c != '\0')
     {
          /* printf("[section char]:%c\n", c); */
          switch(c)
          {
          case '[':
          {
               _name_index = 0;
          }
          break;
          case ']':
          {
               stop_flag = 1;
          }
          break;
          default:
          {
               if(stop_flag) break;
               ret->name[_name_index] = c;
               _name_index++;
          }
          }
          c = *++buf;
     }
     ret->items = NULL;
     ret->next = NULL;
#if 0
     debug_section(ret);
#endif
     return ret;
}

struct section *parse_ini(char *filename){
     // read each line, clear the comment
     FILE *fp;
     if(!(fp = fopen(filename, "r"))){
#ifdef DEBUG
          printf("Open File:[%s]\n", strerror(errno));
#endif
          return NULL;
     }
     ssize_t line_len = 0;
     char *linebuf = (char *)malloc(sizeof(char) * MAX_LINE);
     char *valid_part, *is_section, *section_name, *item_name, *item_value;
     struct section *head, *pos, *last;
     struct item *ipos, *ilast;
     ipos = ilast = head = pos = last = NULL;
     while((line_len = getline(&linebuf, &line_len, fp)) != -1){
#if 0
          printf("[buf type]:%d\n", buf_type(linebuf));
#endif
          switch(buf_type(linebuf))
          {
          case 1:
          {
               continue;
          }
          break;
          case 2:
          {
               //new section
               pos = parse_section(linebuf);
#if 0
               printf("Get Sec:[%s]\n", pos->name);
#endif

               if(head == NULL)
               {
                    last = head = pos;
#if 0
                    debug_section(pos);
#endif
               }
                    
               else
               {
#if 0
                    debug_section(pos);
#endif
                    last->next = pos;
                    last =  last->next;
               }
          }
          break;
          case 3:
          {
               // new item
#if 0
               printf("Current [%s]\n", pos->name);
#endif
               ipos = parse_item(linebuf);
#if 0
               debug_item(ipos);
#endif
               if(!pos->items)
               {
                    pos->items  = ipos;
                    ilast = pos->items;
               }
               else
               {
                    ilast->next = ipos;
                    ilast = ilast->next;
               }
                    
          }
          break;
          }
     }
     struct section *ret = (struct section *)malloc(sizeof(struct section));
     memset(ret, 0, sizeof(struct section));
     /* printf("Final Debug============\n"); */
     /* debug_section(head); */
     fclose(fp);
     return ret;
}


int main(int argc, char **argv){
     parse_ini("test.ini");
     return 0;
}

