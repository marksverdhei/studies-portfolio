
// Value is a void pointer because we want our
// linked list as generic as c allows us to.
// It is designed to e.g. hold both packet pointers
// and character pointers
struct Node {
    void* value;
    struct Node* next;
};

struct Linkedlist {
    int size;
    struct Node* first;
    struct Node* last;
};

struct Linkedlist* Linkedlist_create();

void Linkedlist_append(struct Linkedlist* list, void* value);

void Linkedlist_push(struct Linkedlist* list, void* value);

void* Linkedlist_pop();

void Linkedlist_free();

void Linkedlist_free_full();
