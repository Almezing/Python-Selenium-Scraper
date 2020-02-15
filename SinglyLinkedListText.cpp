/*
Introduction to Singly Linked List implemented in C++
https://www.codesdope.com/blog/article/c-linked-lists-in-c-singly-linked-list/
*/

#include <iostream>

using namespace std;

    //using structures (struct) to represent a node having some data
    //using a pointer (*) to another struct of the same kind
    //pointer holds the address of the next node and creates the link between the 2 nodes
struct node {
    int data;
    node *next;
};

class linked_list{
    private: node *head,*tail;
    public: linked_list(){
        head = NULL;
        tail = NULL;
    }
    void add_node(int n){
        node *tmp = new node;
        tmp -> data = n;
        tmp -> next = NULL;

        if(head == NULL){
            head = tmp;
            tail = tmp;
        }
        else {
            tail -> next = tmp;
            tail = tail -> next;
        }
    }
    
    void display(){
        node *tmp;
        tmp = head;
        while (tmp != NULL){
            cout << tmp -> data << endl;
            tmp = tmp -> next;
        }
    }
};



int main() {
    linked_list a;
    a.add_node(1);
    a.add_node(2);
    a.display();
    return 0;
}
