# Release Notes

## 1.0.3

### Added

- Settings to override the serializers on the views by using a custom.
- `EditMessageApiView` allowing editing a message sent from a user of a given thread.
- `CurrentThreadDefault` similar to `CurrentUserDefault` from Django Rest Framework but for threads. 

### Fixed

- Show sender when a message sent is from the same sender and receiver - [Issue](https://github.com/tarsil/django-messages-drf/issues/5)
- Issue with `display_name` for InboxSerializer - [Issue](https://github.com/tarsil/django-messages-drf/issues/4).
- `ThreadCRUDApiView` `post` where wasn't using the data from the serializer.

## 1.0.2

### Added

- Support for python 3.9
- CircleCI config

### Fixed

- Tests naming conflicts.
- Migration issues.

### Updated

- README.

## 1.0.0

- Initial release

## License

Copyright (c) 2020-present Tiago Silva and contributors under the [MIT license](https://opensource.org/licenses/MIT).