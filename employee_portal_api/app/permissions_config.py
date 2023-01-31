role_based_permissions = {
    'PlatformAdmin': [{
        'Product': ['list', 'create', 'retrieve'],
        'Reservation': ['list', 'create', 'retrieve', 'destroy'],
        'Cart': ['list', 'retrieve'],
        'CartItem': ['list', 'retrieve'],
        'Order': ['list', 'retrieve'],
        'OrderStatusHistory': ['list', 'retrieve'],
        'OrderItem': ['list', 'retrieve'],
        'PaymentGateway': ['list', 'create', 'retrieve'],
        'Payment': ['list', 'retrieve'],
        'PaymentTransaction': ['list', 'retrieve'],
        'PaymentGatewayConfig': ['list', 'create', 'retrieve'],
        'StorePaymentGateway': ['list', 'create', 'retrieve'],
        'Enrollment': ['list', 'retrieve'],
        'EnrollmentStatusHistory': ['list', 'retrieve'],
        'ProfileSavedCareer': ['list', 'retrieve'],
        'ProfileCareerQuiz': ['list', 'retrieve'],
        'Profile': ['list', 'retrieve'],
        'IdentityProvider': ['list', 'create', 'retrieve'],
        'ProfileLink': ['list', 'retrieve'],
        'ProfileCommunicationMedium': ['list', 'retrieve'],
        'ProfilePreference': ['list', 'retrieve'],
        'ProfileStore': ['list', 'retrieve'],
        'CourseProvider': ['list', 'create', 'retrieve'],
        'Course': ['list', 'retrieve'],
        'Section': ['list', 'retrieve'],
        'StoreCourse': ['list', 'retrieve'],
        'Store': ['list', 'create', 'retrieve'],
        'StoreFeaturedCareer': ['list', 'retrieve'],
        'StoreIdentityProvider': ['list', 'create', 'retrieve'],
        'CustomUser': ['list', 'create', 'retrieve'],
        'Role': ['list', 'create', 'retrieve'],
    }],
    'CourseAdmin': [{
        'Order': ['list', 'retrieve'],
        'OrderStatusHistory': ['list', 'retrieve'],
        'OrderItem': ['list', 'retrieve'],
        'Payment': ['list', 'retrieve'],
        'PaymentTransaction': ['list', 'retrieve'],
        'Enrollment': ['list', 'retrieve'],
        'EnrollmentStatusHistory': ['list', 'retrieve'],
        'ProfileSavedCareer': ['list', 'retrieve'],
        'ProfileCareerQuiz': ['list', 'retrieve'],
        'Profile': ['list', 'retrieve'],
        'ProfileLink': ['list', 'retrieve'],
        'ProfileCommunicationMedium': ['list', 'retrieve'],
        'ProfilePreference': ['list', 'retrieve'],
        'ProfileStore': ['list', 'retrieve'],
        'CourseProvider': ['list', 'retrieve'],
        'Course': ['list', 'create', 'retrieve'],
        'Section': ['list', 'create', 'retrieve'],
    }],
    'StoreAdmin': [{
        'Order': ['list', 'retrieve'],
        'OrderStatusHistory': ['list', 'retrieve'],
        'OrderItem': ['list', 'retrieve'],
        'PaymentGateway': ['list', 'retrieve'],
        'Payment': ['list', 'retrieve'],
        'PaymentTransaction': ['list', 'retrieve'],
        'PaymentGatewayConfig': ['list', 'retrieve'],
        'StorePaymentGateway': ['list', 'retrieve'],
        'Enrollment': ['list', 'retrieve'],
        'EnrollmentStatusHistory': ['list', 'retrieve'],
        'ProfileSavedCareer': ['list', 'retrieve'],
        'ProfileCareerQuiz': ['list', 'retrieve'],
        'Profile': ['list', 'retrieve'],
        'IdentityProvider': ['list', 'retrieve'],
        'ProfileLink': ['list', 'retrieve'],
        'ProfileCommunicationMedium': ['list', 'retrieve'],
        'ProfilePreference': ['list', 'retrieve'],
        'ProfileStore': ['list', 'retrieve'],
        'CourseProvider': ['list', 'retrieve'],
        'Course': ['list', 'retrieve'],
        'Section': ['list', 'retrieve'],
        'StoreCourse': ['list', 'create', 'retrieve'],
        'Store': ['list', 'retrieve'],
        'StoreFeaturedCareer': ['list', 'create', 'retrieve'],
        'StoreIdentityProvider': ['list', 'retrieve'],
    }],
}
