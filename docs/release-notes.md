# Release Notes

## 1.0.6

- Preparing to drop support for python 3.6.
- Fix `providing_args` from signals as it is deprecated in Django 4.

## 1.0.5

- Added `id` field to the ThreadSerializer.

## 1.0.4

- [Bugfix #10](https://github.com/tarsil/django-messages-drf/pull/10). Thank you [kamikaz1k](https://github.com/kamikaz1k)
- [Bugfix #9](https://github.com/tarsil/django-messages-drf/pull/9). Thank you [kamikaz1k](https://github.com/kamikaz1k)

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
