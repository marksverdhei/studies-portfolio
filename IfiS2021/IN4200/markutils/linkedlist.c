#include <stdlib.h>
#include "linkedlist.h"

struct Node* Node_create(void* value) {
    struct Node* node = malloc(sizeof(struct Node));
    node->value = value;
    node->next = NULL;
    return node;
}

struct Linkedlist* Linkedlist_create() {
    struct Linkedlist* list = malloc(sizeof(struct Linkedlist));
    list->size = 0;
    list->first = NULL;
    list->last = NULL;
    return list;
}

void Linkedlist_append(struct Linkedlist* list, void* value) {
    struct Node* new_node = Node_create(value);
    if (list->last != NULL) list->last->next = new_node;
    list->last = new_node;

    if (list->first == NULL) list->first = list->last;
    list->size++;
}

void Linkedlist_push(struct Linkedlist* list, void* value) {
    struct Node* new_node = Node_create(value);
    if (list->first != NULL) new_node->next = list->first;
    list->first = new_node;

    if (list->last == NULL) list->last = list->first;
    list->size++;
}

void* Linkedlist_pop(struct Linkedlist* list) {
    struct Node* old_first = list->first;
    if (old_first != NULL) {
        void* ret = old_first->value;
        struct Node* new_first = list->first->next;

        if (new_first != NULL) list->first = new_first;
        else list->first = NULL;
        list->size--;

        free(old_first);
        return ret;
    } else return NULL;
}

void Linkedlist_free(struct Linkedlist* list) {
    while (list->size > 0) Linkedlist_pop(list);
    free(list);
}

void Linkedlist_free_full(struct Linkedlist* list) {
    while (list->size > 0) free(Linkedlist_pop(list));
    free(list);
}
