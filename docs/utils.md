# Utils

Some useful utils are provided with the project to make it easier to reuse across.

---

1. [AuditModel](#auditmodel)

---

## AuditModel

```python
class AuditModel(models.Model):
    """A common audit model for tracking"""
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)

```

Adding the **`AuditModel`** to a model will add an audit trailing to it making it easier
to filter by dates.

This can be extended and add more information such as **`created_by`** or **`modified_by`**
where those are users of the application.
