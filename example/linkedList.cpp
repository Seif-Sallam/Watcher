#include <iostream>
#include <string>
#include <sstream>

template<typename T = int>
struct Node
{
    T data;
    Node* next;
    Node* prev;
};

template<typename T = int>
struct LinkedList
{
    Node<T>* head;
    Node<T>* tail;
    size_t size;
};

template<typename T = int>
void
ll_push_front(LinkedList<T>& self, T data)
{
    if (self.size == 0)
    {
        self.head = new Node<T>{};
        self.head->data = data;
        self.tail = self.head;
        self.size += 1;
        return;
    }

    auto newNode = new Node<T>{};
    newNode->data = data;
    newNode->next = self.head;
    self.head->prev = newNode;
    newNode->prev = nullptr;
    self.head = newNode;
    self.size += 1;
}

template<typename T>
void
ll_push_back(LinkedList<T>& self, T data)
{
    if (self.size == 0)
    {
        self.head = new Node<T>{};
        self.head->data = data;
        self.tail = self.head;
        self.size += 1;
        return;
    }

    auto newNode = new Node<T>{};
    newNode->data = data;
    newNode->prev = self.tail;
    self.tail->next = newNode;
    self.tail = newNode;
    self.size += 1;
}

template<typename T>
void
ll_traverse(LinkedList<T>& self, void(*func)(T& data))
{
    auto node = self.head;
    while (node)
    {
        func(node->data);
        node = node->next;
    }
}

template<typename T>
void
ll_rev_traverse(LinkedList<T>& self, void(*func)(T& data))
{
    auto node = self.tail;
    while (node)
    {
        func(node->data);
        node = node->prev;
    }
}

template<typename T>
void
ll_insert(LinkedList<T>& self, size_t pos, T data)
{
    if (self.size <= pos)
    {
        ll_push_back(self, data);
        return;
    }
    if (self.size <= 0)
    {
        ll_push_front(self, data);
        return;
    }

    auto current = self.head;
    for (int i = 0; i < pos - 1; ++i, current = current->next);

    auto newNode = new Node<T>{};
    newNode->data = data;
    newNode->next = current->next;
    current->next->prev = newNode;
    newNode->prev = current;
    current->next = newNode;
    self.size += 1;
}

template<typename T>
void
print_ll(LinkedList<T>& self)
{
    std::cout << "[ *";
    ll_traverse<int>(self, [](auto& data){
        std::cout << " -> " << data;
    });
    std::cout << " ]\n";
}

template<typename T>
void
print_rev_ll(LinkedList<T>& self)
{
    std::cout << "[ *";
    ll_rev_traverse<int>(self, [](auto& data){
        std::cout << " -> " << data;
    });
    std::cout << " ]\n";
}

int main()
{
    LinkedList<int> ll{};
    ll_insert(ll, 2, 1);
        print_ll(ll);
        print_rev_ll(ll);
    ll_insert(ll, 2, 3);
        print_ll(ll);
        print_rev_ll(ll);
    ll_insert(ll, 2, 4);
        print_ll(ll);
        print_rev_ll(ll);
    ll_insert(ll, 2, 2);
        print_ll(ll);
        print_rev_ll(ll);
    ll_insert(ll, 2, 2);
        print_ll(ll);
        print_rev_ll(ll);

    return 0;
}