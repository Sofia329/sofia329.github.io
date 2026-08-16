// output type need to be a pointer to a struct ListNode type, the input type need to be an integer type, this is a function to create a single node

struct ListNode* createSingleNode(int val)
{
    struct ListNode *ptr = malloc (sizeof(struct ListNode));
    if (ptr == NULL)
    {
        return NULL;
    }
    ptr -> val = val;
    ptr -> next = NULL;
    return ptr;
}

void printList(struct ListNode *head)
{
    while (head)
    {
        printf("%i", head->val);
        head = head->next;
    }
}

struct ListNode* appendNode(struct ListNode *head, int val)
{
    if (head == NULL)
    {
        struct ListNode *node = malloc (sizeof(struct ListNode));
        if (node == NULL)
        {
            return NULL;
        }
        node -> val = val;
        node -> next = NULL;
        return node;
    }
    else
    {
       struct ListNode *ptr = head;
       while (ptr -> next != NULL)
       {
        ptr = ptr -> next;
       }

       struct ListNode *node = malloc (sizeof(struct ListNode));
       if (node == NULL)
       {
        return NULL;
       }
       node -> val = val;
       ptr -> next = node;
       return head;
    }

}



//Leetcode Add Two Numbers

/*
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */

 #include <stdbool.h>

struct ListNode* addTwoNumbers(struct ListNode* l1, struct ListNode* l2) {

    struct ListNode *output = malloc (sizeof(struct ListNode));

    if (output == NULL)
    {
        return NULL;
    }

    struct ListNode *pointer = output;

    // at least 1 node for both l1 and l2, so the first access val of l1 and l2 not necessary to check if node is NULL

    int first_number_digit = l1 -> val;
    int second_number_digit = l2 -> val;
    int result = first_number_digit + second_number_digit;
    bool carry = false;

    while (l1 || l2)
    {
        if (carry)
        {
            result ++;
        }

        if (result >= 10)
        {
            pointer -> val = result % 10;
            carry = true;

        }
        else
        {
            pointer -> val = result;
            carry = false;
        }

        // create a new node to be the next node for output
        // insert the new node into output's 尾部

        if ((l1 != NULL && l1 -> next) || (l2!= NULL && l2 -> next))
        {
            struct ListNode *node = malloc (sizeof(struct ListNode));

            if (node == NULL)
            {
                return NULL;
            }

            pointer -> next = node;
            pointer = pointer -> next;

        }


        // update to the next node of L1 and L2

        if (l1)
        {
            l1 = l1 -> next;
            first_number_digit = (l1 != NULL) ? l1 -> val : 0;
        }

        else
        {
            first_number_digit = 0;
        }

        if (l2)
        {
            l2 = l2 -> next;
            second_number_digit = (l2 != NULL) ? l2 -> val : 0;
        }

        else
        {
            second_number_digit = 0;
        }

        result = first_number_digit + second_number_digit;

    }
    if (carry)
    {

    }
    return output;
}
