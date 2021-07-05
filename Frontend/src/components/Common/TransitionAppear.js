import React from 'react';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';

const DEFAULT_DURATION = 1000;

class FakeTransitionWrapper extends React.Component
{
    constructor(props)
    {
        super(props);
    }

    render()
    {
        const children = React.Children.toArray(this.props.children);

        return children[0] || null;
    }
}

export default class TransitionAppear extends React.Component
{
    constructor(props)
    {
        super(props);
    }

    render()
    {
        const props = this.props;
        const duration = props.hasOwnProperty('duration') ? props.duration : DEFAULT_DURATION;

        return (
            <ReactCSSTransitionGroup
                component={FakeTransitionWrapper}
                transitionName='transition'
                transitionAppear={Boolean(duration)}
                transitionAppearTimeout={duration}
                transitionEnter={false}
                transitionLeave={false}
            >
                {this.props.children}
            </ReactCSSTransitionGroup>
        );
    }
}
